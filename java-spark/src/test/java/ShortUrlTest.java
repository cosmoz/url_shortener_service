import org.junit.jupiter.api.*;
import redis.clients.jedis.Jedis;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import static org.junit.jupiter.api.Assertions.*;

class ShortUrlTest {
    static final int PORT = 5051;
    static final String BASE = "http://localhost:" + PORT;
    static final HttpClient http = HttpClient.newBuilder()
        .followRedirects(HttpClient.Redirect.NEVER)
        .build();
    static Jedis redis;

    @BeforeAll
    static void setup() {
        redis = new Jedis("localhost", 6379);
        ShortUrl.start(PORT);
    }

    @AfterAll
    static void teardown() {
        spark.Spark.stop();
        spark.Spark.awaitStop();
        redis.close();
    }

    HttpResponse<String> get(String path) throws Exception {
        return http.send(HttpRequest.newBuilder(URI.create(BASE + path)).GET().build(),
            HttpResponse.BodyHandlers.ofString());
    }

    HttpResponse<String> postForm(String path, String body) throws Exception {
        return http.send(HttpRequest.newBuilder(URI.create(BASE + path))
            .header("Content-Type", "application/x-www-form-urlencoded")
            .POST(HttpRequest.BodyPublishers.ofString(body)).build(),
            HttpResponse.BodyHandlers.ofString());
    }

    @Test
    void mainPage() throws Exception {
        assertEquals(200, get("/").statusCode());
    }

    @Test
    void redirectMissingKey() throws Exception {
        redis.del("12345");
        assertEquals(404, get("/12345").statusCode());
    }

    @Test
    void redirectExistingKey() throws Exception {
        redis.set("12345", "https://example.com");
        assertEquals(302, get("/12345").statusCode());
    }

    @Test
    void shortenBadUrl() throws Exception {
        assertEquals(400, postForm("/shorten/", "url=not-a-url").statusCode());
    }

    @Test
    void shortenEmptyUrl() throws Exception {
        assertEquals(400, postForm("/shorten/", "url=").statusCode());
    }

    @Test
    void shortenValidUrl() throws Exception {
        var r = postForm("/shorten/", "url=https://example.com");
        assertEquals(200, r.statusCode());
        assertFalse(r.body().isBlank());
    }

    @Test
    void shortenSameUrlSameKey() throws Exception {
        var r1 = postForm("/shorten/", "url=https://example.com/path");
        var r2 = postForm("/shorten/", "url=https://example.com/path");
        assertEquals(r1.body(), r2.body());
    }

    @Test
    void shortenKeyIsUnsigned() throws Exception {
        var r = postForm("/shorten/", "url=https://example.com");
        long key = Long.parseLong(r.body().trim());
        assertEquals(key, key & 0xFFFFFFFFL);
    }
}
