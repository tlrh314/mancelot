server {
    listen 80;
    listen [::]:80;

    server_name pw.mancelot.nl;

    include /etc/nginx/apps/well-known.conf;
    include /etc/nginx/apps/cloudflare.conf;

    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name pw.mancelot.nl;

    ssl_certificate /etc/letsencrypt/live/pw.mancelot.nl/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/pw.mancelot.nl/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    include /etc/nginx/apps/well-known.conf;
    include /etc/nginx/apps/cloudflare.conf;

    location / {
        add_header Content-Type text/plain;
        return 200 "pw.mancelot.nl";
    }

    # location /server {
    #     rewrite ^/server/(.*) /$1 break;
    #     proxy_set_header    Host $host;
    #     proxy_set_header    X-Real-IP $remote_addr;
    #     proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
    #     proxy_set_header    X-Forwarded-Proto $scheme;

    #     proxy_pass          http://psono-server:80;
    # }

    # location / {
    #     proxy_set_header    Host $host;
    #     proxy_set_header    X-Real-IP $remote_addr;
    #     proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
    #     proxy_set_header    X-Forwarded-Proto $scheme;

    #     proxy_pass          http://psono-client:80;
    #     proxy_read_timeout  90;
    #     proxy_redirect      http://psono-client:80 /;
    # }
}
