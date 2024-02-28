FROM rocker/rstudio

RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    tdsodbc \
    libsqliteodbc \
    gnupg \
    unixodbc \
    unixodbc-dev \
    ## clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/ \
    && rm -rf /tmp/downloaded_packages/ /tmp/*.rds

RUN wget https://downloads.mysql.com/archives/get/p/10/file/mysql-connector-odbc-8.0.19-linux-debian9-x86-64bit.tar.gz \
 && tar xvf mysql-connector-odbc-8.0.19-linux-debian9-x86-64bit.tar.gz \
 && cp mysql-connector-odbc-8.0.19-linux-debian9-x86-64bit/bin/* /usr/local/bin \
 && cp mysql-connector-odbc-8.0.19-linux-debian9-x86-64bit/lib/* /usr/local/lib \
 && sudo apt-get update \
 && apt-get install --yes libodbc1 odbcinst1debian2 \
 && chmod 777 /usr/local/lib/libmy*

RUN myodbc-installer -a -d -n "MySQL ODBC 8.0 Driver" -t "Driver=/usr/local/lib/libmyodbc8w.so" \
 && myodbc-installer -a -d -n "MySQL ODBC 8.0" -t "Driver=/usr/local/lib/libmyodbc8a.so"

RUN Rscript -e 'install.packages(c("DBI","odbc"))'
