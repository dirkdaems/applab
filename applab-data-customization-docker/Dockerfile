FROM centos

# Create group and user
RUN groupadd worker
RUN useradd --create-home --home-dir /home/worker -g worker worker

# Set working directory
WORKDIR /home/worker

# Copy AppLab scripts
COPY applab /home/worker/applab

# Install packages
RUN yum update  -y                      && \
    yum install -y gcc-c++              && \
    yum install -y epel-release.noarch  && \
    yum install -y gdal                 && \
    yum install -y gdal-devel           && \
    yum install -y gdal-libs            && \
    yum install -y proj                 && \
    yum install -y proj-devel           && \
    yum install -y proj-epsg            && \
    yum install -y proj-nad             && \
    yum install -y gdal-python          && \
    yum install -y python-pip           && \
    yum install -y python-devel         && \
    yum install -y ftp                  && \
    yum install -y lftp                 && \
    pip install -U pip                  && \
    pip install pyproj                  && \
    pip install enum                    && \
    pip install scipy                   && \
    pip install --index-url https://artifactory.vgt.vito.be/api/pypi/python-packages/simple catalogclient

# Set default username
USER root

