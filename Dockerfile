FROM ubuntu:16.04
MAINTAINER aheimberger


# setup default build arguments
ARG SYSTEMC_VERSION=systemc-2.3.0a
ARG GROUP_ID=1000
ARG USER_ID=1000
ARG USER_NAME=travisci


# prerequisites
RUN apt-get -qq update && \
	apt-get -qq dist-upgrade && \
	\
	apt-get install -qq -y --no-install-recommends \
	git \
	openssl \
	ca-certificates \
	wget \
	tar \
	build-essential \
	gdb \
	python3 \
	python3-pip && \
	\
	pip3 install --upgrade pip && \
	pip3 install numpy


# setup environment directories
ENV DIR_HOME		/home/${USER_NAME}
ENV DIR_DEPLOY		${DIR_HOME}/deploy
ENV DIR_PROJECT		${DIR_HOME}/project
ENV SYSTEMC_HOME	/opt/${SYSTEMC_VERSION}


# lets get systemc
RUN echo -e "SYSTEMC_VERSION ${SYSTEMC_VERSION}" && \
	echo -e "SYSTEMC_HOME ${SYSTEMC_HOME}\n\n" && \
	cd /tmp && \
	wget http://accellera.org/images/downloads/standards/systemc/${SYSTEMC_VERSION}.tar.gz && \
	tar xvf ${SYSTEMC_VERSION}.tar.gz && \
	rm ${SYSTEMC_VERSION}.tar.gz && \
	cd ${SYSTEMC_VERSION} && \
	mkdir objdir && \
	cd objdir && \
	mkdir -p ${SYSTEMC_HOME} && \
	export CXX=g++ && \
	../configure --enable-debug --prefix=${SYSTEMC_HOME} && \
	make && \
	make install && \
	cd ../.. && \
	rm -rfv ${SYSTEMC_VERSION}


# lets create the user
RUN groupadd -g "${GROUP_ID}" "${USER_NAME}" && \
    useradd -u ${USER_ID} -g ${GROUP_ID} -ms /bin/bash ${USER_NAME}


# setup directories
RUN mkdir -p ${DIR_DEPLOY} && \
	mkdir -p ${DIR_PROJECT}


# test it locally
COPY . ${DIR_PROJECT}


# change permissions
RUN chown -R ${USER_NAME}:${USER_NAME} ${DIR_DEPLOY} && \
	chown -R ${USER_NAME}:${USER_NAME} ${DIR_PROJECT}


# change user
USER ${USER_NAME}


# lets create the .gdbinit file
RUN echo "python\n\
import sys, os\n\
\n\
home = os.path.expanduser(\"~\")\n\
\n\
sys.path.insert(0, home + '/project/systemc23/')\n\
from systemc23printers import register_systemc23_printers\n\
register_systemc23_printers (None)\n\
\n\
end" > ${DIR_HOME}/.gdbinit


# setup the working directory
WORKDIR ${DIR_PROJECT}


# setup entrypoint function
ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD ["help"]
