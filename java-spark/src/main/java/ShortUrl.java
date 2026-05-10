import static spark.Spark.*;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import java.util.zip.CRC32;

public class ShortUrl {
    static final JedisPool pool = new JedisPool("localhost", 6379);

    public static void main(String[] args) {
        start(Integer.parseInt(System.getenv().getOrDefault("PORT", "5050")));
    }

    static void start(int p) {
        port(p);

        get("/", (req, res) -> new String(ShortUrl.class.getResourceAsStream("/index.html").readAllBytes()));

        get("/:key", (req, res) -> {
            try (Jedis r = pool.getResource()) {
                String url = r.get(req.params("key"));
                if (url == null) { res.status(404); return "Not found"; }
                res.status(302);
                res.header("Location", url);
                return "";
            }
        });

        post("/shorten/", (req, res) -> {
            String url = req.queryParams("url");
            if (url == null || !url.contains("://")) { res.status(400); return "Bad URL"; }
            CRC32 crc = new CRC32();
            crc.update(url.getBytes());
            long key = crc.getValue();
            try (Jedis r = pool.getResource()) {
                r.set(String.valueOf(key), url);
            }
            return String.valueOf(key);
        });

        awaitInitialization();
    }
}
