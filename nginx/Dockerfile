FROM nginx:1.17-alpine

# Remove the default configuration files
RUN rm /etc/nginx/conf.d/*

# Insert our own configuration files
COPY conf/*.conf /etc/nginx/conf.d/
COPY apps/*.conf /etc/nginx/apps/
