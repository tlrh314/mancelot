server {
    listen 80;
    listen [::]:80;

    server_name mm.mancelot.nl;
    server_tokens off;

    include /etc/nginx/apps/well-known.conf;
    include /etc/nginx/apps/cloudflare.conf;

    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name mm.mancelot.nl;
    server_tokens off;

    ssl_certificate /etc/letsencrypt/live/mm.mancelot.nl/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mm.mancelot.nl/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    include /etc/nginx/apps/well-known.conf;
    include /etc/nginx/apps/cloudflare.conf;

    location / {
        add_header Content-Type text/plain;
        return 200 "mm.mancelot.nl";
    }
}
