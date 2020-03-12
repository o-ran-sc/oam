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

package org.oransc.oam.features.devicemanager.xran.impl;

import java.util.Optional;
import org.eclipse.jdt.annotation.NonNull;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.ne.factory.NetworkElementFactory;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.ne.service.NetworkElement;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.service.DeviceManagerServiceProvider;
import org.onap.ccsdk.features.sdnr.wt.netconfnodestateservice.NetconfAccessor;
import org.opendaylight.yang.gen.v1.urn.xran.hardware._1._0.rev180720.XRANRADIO;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class XRanNetworkElementFactory implements NetworkElementFactory {

    private static final Logger log = LoggerFactory.getLogger(XRanNetworkElementFactory.class);

    @Override
    public Optional<NetworkElement> create(@NonNull NetconfAccessor acessor, @NonNull DeviceManagerServiceProvider serviceProvider) {
        if (acessor.getCapabilites().isSupportingNamespace(XRANRADIO.QNAME)) {
            log.info("Create device {} ",XRanNetworkElement.class.getName());
            return Optional.of(new XRanNetworkElement(acessor, serviceProvider.getDataProvider()));
        } else {
            return Optional.empty();
        }
    }
}
