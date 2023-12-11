FROM ibmcom/websphere-traditional:8.5.5.24-ubi8
COPY app.ear /work/config/app.ear
COPY install_app.py /work/config/install_app.py
COPY was-config.props /work/config/was-config.props
RUN /work/configure.sh
