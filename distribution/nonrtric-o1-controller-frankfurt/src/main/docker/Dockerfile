# Base odl alpine with added packages needed for
FROM ${base.image.repo}

# Image info
ENV IMAGEPATH ${IMAGEPATH}//${image.name}
ENV IMAGENAMES ${IMAGENAMES}//"ORAN nonrtric"

# Adjust repo und feature boot info for karaf
RUN sed -i -e "\|featuresRepositories|s|$|,${features.repo}|"  $ODL_HOME/etc/org.apache.karaf.features.cfg
ENV SDNRWT_BOOTFEATURES ${features.boot}

USER root
# copy CCSDK mvn artifacts to ODL repository
COPY system /tmp/system
RUN rsync -a /tmp/system $ODL_HOME && rm -rf /tmp/system
RUN chown -R odl:odl $ODL_HOME

# Set user for ODL startup
USER odl
