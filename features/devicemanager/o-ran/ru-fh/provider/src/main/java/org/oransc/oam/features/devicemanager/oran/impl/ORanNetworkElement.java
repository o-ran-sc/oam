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

import java.util.List;
import java.util.Optional;
import org.eclipse.jdt.annotation.NonNull;
import org.onap.ccsdk.features.sdnr.wt.dataprovider.model.DataProvider;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.ne.service.NetworkElement;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.ne.service.NetworkElementService;
import org.onap.ccsdk.features.sdnr.wt.netconfnodestateservice.NetconfAccessor;
import org.opendaylight.mdsal.common.api.LogicalDatastoreType;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.hardware.rev180313.Hardware;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.hardware.rev180313.hardware.Component;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.data.provider.rev190801.NetworkElementDeviceType;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.NodeId;
import org.opendaylight.yangtools.concepts.ListenerRegistration;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.opendaylight.yangtools.yang.binding.NotificationListener;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 */
public class ORanNetworkElement implements NetworkElement {

    private static final Logger log = LoggerFactory.getLogger(ORanNetworkElement.class);

    private final NetconfAccessor netconfAccessor;

    private final DataProvider databaseService;

    private final ORanToInternalDataModel oRanMapper;

    private ListenerRegistration<NotificationListener> oRanListenerRegistrationResult;
    private @NonNull final ORanChangeNotificationListener oRanListener;
    private ListenerRegistration<NotificationListener> oRanFaultListenerRegistrationResult;
    private @NonNull final ORanFaultNotificationListener oRanFaultListener;

    ORanNetworkElement(NetconfAccessor netconfAccess, DataProvider databaseService) {
        log.info("Create {}",ORanNetworkElement.class.getSimpleName());
        this.netconfAccessor = netconfAccess;
        this.databaseService = databaseService;

        this.oRanListenerRegistrationResult = null;
        this.oRanListener = new ORanChangeNotificationListener(netconfAccessor, databaseService);

        this.oRanFaultListenerRegistrationResult = null;
        this.oRanFaultListener = new ORanFaultNotificationListener();

        this.oRanMapper = new ORanToInternalDataModel();

    }

    public void initialReadFromNetworkElement() {
        Hardware hardware = readHardware(netconfAccessor);
        if (hardware != null) {
            List<Component> componentList = hardware.getComponent();
            if (componentList != null) {
                for (Component component : componentList) {
                    databaseService.writeInventory( oRanMapper.getInternalEquipment(netconfAccessor.getNodeId(), component));
                }
            }
        }
    }

    @Override
    public NetworkElementDeviceType getDeviceType() {
        return NetworkElementDeviceType.ORAN;
    }

    private Hardware readHardware(NetconfAccessor accessData) {

        final Class<Hardware> clazzPac = Hardware.class;

        log.info("DBRead Get equipment for class {} from mountpoint {} for uuid {}", clazzPac.getSimpleName(),
                accessData.getNodeId().getValue());

        InstanceIdentifier<Hardware> hardwareIID =
                InstanceIdentifier.builder(clazzPac).build();

        Hardware res = accessData.getTransactionUtils().readData(accessData.getDataBroker(), LogicalDatastoreType.OPERATIONAL,
                hardwareIID);

        return res;
    }

    @Override
    public void register() {

        initialReadFromNetworkElement();
        // Register call back class for receiving notifications
        this.oRanListenerRegistrationResult = netconfAccessor.doRegisterNotificationListener(oRanListener);
        this.oRanFaultListenerRegistrationResult = netconfAccessor.doRegisterNotificationListener(oRanFaultListener);
        // Register netconf stream
        netconfAccessor.registerNotificationsStream(NetconfAccessor.DefaultNotificationsStream);


    }

    @Override
    public void deregister() {
        if (oRanListenerRegistrationResult != null) {
            this.oRanListenerRegistrationResult.close();
        }
        if (oRanFaultListenerRegistrationResult != null) {
            this.oRanFaultListenerRegistrationResult.close();
        };
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
    public void warmstart() {
    }

    @Override
    public Optional<NetconfAccessor> getAcessor() {
        return Optional.of(netconfAccessor);
    }

}
