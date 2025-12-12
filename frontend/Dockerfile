FROM nginx:alpine

COPY frontend/templates/ /usr/share/nginx/html/
COPY frontend/static/ /usr/share/nginx/html/static/

COPY deployment/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
