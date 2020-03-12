# Base odl alpine with added packages needed for
FROM ${base.image.repo}
ENV SDNR_ORAN_REPO ${features.repo}
RUN sed -i -e "\|featuresRepositories|s|$|,${SDNR_ORAN_REPO}|"  $ODL_HOME/etc/org.apache.karaf.features.cfg
ENV SDNRWT_BOOTFEATURES ${features.boot}

USER root
# copy CCSDK mvn artifacts to ODL repository
COPY system /tmp/system
RUN rsync -a /tmp/system $ODL_HOME && rm -rf /tmp/system
RUN chown -R odl:odl $ODL_HOME

# Set user for ODL startup
USER odl
