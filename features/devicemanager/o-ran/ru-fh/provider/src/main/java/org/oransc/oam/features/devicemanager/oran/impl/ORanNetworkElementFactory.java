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

package org.oransc.oam.features.devicemanager.oran.impl;

import java.util.Optional;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.ne.factory.NetworkElementFactory;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.ne.service.NetworkElement;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.service.DeviceManagerServiceProvider;
import org.onap.ccsdk.features.sdnr.wt.netconfnodestateservice.NetconfAccessor;
import org.opendaylight.yang.gen.v1.urn.o.ran.hardware._1._0.rev190328.ORANHWCOMPONENT;
import org.opendaylight.yang.gen.v1.urn.onf.params.xml.ns.yang.network.topology.simulator.rev191025.SimulatorStatus;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ORanNetworkElementFactory implements NetworkElementFactory {

    private static final Logger log = LoggerFactory.getLogger(ORanNetworkElementFactory.class);

    @Override
    public Optional<NetworkElement> create(NetconfAccessor acessor, DeviceManagerServiceProvider serviceProvider) {
        if (acessor.getCapabilites().isSupportingNamespace(ORANHWCOMPONENT.QNAME)) {
            log.info("Create device {} ",ORanNetworkElement.class.getName());
            return Optional.of(new ORanNetworkElement(acessor, serviceProvider.getDataProvider()));
        } else if (acessor.getCapabilites().isSupportingNamespace(SimulatorStatus.QNAME)) {
            log.info("Create device {} ",NtsNetworkElement.class.getName());
            return Optional.of(new NtsNetworkElement(acessor, serviceProvider.getDataProvider()));
        } else {
            return Optional.empty();
        }
    }
}
