FROM ubuntu:16.04
MAINTAINER aheimberger


# setup default build arguments
ARG SYSTEMC_VERSION=systemc-2.3.0a
ARG USER_ID=no-id
ARG USER_NAME=travisci
ARG GIT_BRANCH=master
ARG GIT_URL=https://github.com/AHeimberger/SystemC-2.3-Pretty-Printer.git
ARG GIT_HASH=no-hash


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


# lets get systemc in /opt
RUN echo -e "SYSTEMC_VERSION ${SYSTEMC_VERSION}" && \
	echo -e "SYSTEMC_HOME ${SYSTEMC_HOME}\n\n" && \
	cd /tmp && \
	wget http://accellera.org/images/downloads/standards/systemc/${SYSTEMC_VERSION}.tar.gz && \
	tar xvf ${SYSTEMC_VERSION}.tar.gz && \
	rm ${SYSTEMC_VERSION}.tar.gz && \
	cd ${SYSTEMC_VERSION} && \
	mkdir objdir && \
	cd objdir && \
	export CXX=g++ && \
	../configure --prefix=${SYSTEMC_HOME} && \
	make && \
	make install && \
	make check && \
	cd ../.. && \
	rm -rf ${SYSTEMC_VERSION}


# lets create the user
RUN useradd -ms /bin/bash ${USER_NAME}
USER ${USER_NAME}


# setup directories
RUN mkdir -p ${DIR_DEPLOY} && \
	mkdir -p ${DIR_PROJECT}


# lets checkout the repository use https because of ssh key verification
RUN git clone -b ${GIT_BRANCH} ${GIT_URL} ${DIR_PROJECT} && \
	if [ ${GIT_HASH} != "no-hash" ]; then cd ${DIR_PROJECT} && git reset --hard ${GIT_HASH}; fi


# setup the working directory
WORKDIR ${DIR_HOME}


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
end" > .gdbinit
