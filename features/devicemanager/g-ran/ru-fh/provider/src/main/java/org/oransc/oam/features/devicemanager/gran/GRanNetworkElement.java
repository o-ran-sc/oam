/*
 * ============LICENSE_START========================================================================
 * ONAP : ccsdk feature sdnr wt
 * =================================================================================================
 * Copyright (C) 2019 highstreet technologies GmbH Intellectual Property. All rights reserved.
 * =================================================================================================
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 * ============LICENSE_END==========================================================================
 */
package org.oransc.oam.features.devicemanager.gran;

import java.util.Optional;
import org.onap.ccsdk.features.sdnr.wt.dataprovider.model.DataProvider;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.ne.service.NetworkElement;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.ne.service.NetworkElementService;
import org.onap.ccsdk.features.sdnr.wt.netconfnodestateservice.NetconfAccessor;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.data.provider.rev190801.NetworkElementDeviceType;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.NodeId;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * @author herbert
 *
 */
public class GRanNetworkElement implements NetworkElement {

    private static final Logger log = LoggerFactory.getLogger(GRanNetworkElement.class);

    private final NetconfAccessor netconfAccessor;
    @SuppressWarnings("unused")
    private final DataProvider databaseService;

    public GRanNetworkElement(NetconfAccessor netconfAccess, DataProvider databaseService) {
        log.info("Create {}", GRanNetworkElement.class.getSimpleName());
        this.netconfAccessor = netconfAccess;
        this.databaseService = databaseService;
    }

    @Override
    public void register() {
        log.info("Register actions should be here");
    }

    @Override
    public void deregister() {
        log.info("deRegister actions should be here");
    }

    @Override
    public void warmstart() {
        log.info("Warmstart actions should be here");
    }

    @Override
    public NodeId getNodeId() {
        return netconfAccessor.getNodeId();
    }

    @Override
    public <L extends NetworkElementService> Optional<L> getService(Class<L> clazz) {
        return Optional.empty();
    }

    @Override
    public NetworkElementDeviceType getDeviceType() {
        return NetworkElementDeviceType.RAN3GPP;
    }

    @Override
    public Optional<NetconfAccessor> getAcessor() {
        return Optional.of(netconfAccessor);
    }

}
