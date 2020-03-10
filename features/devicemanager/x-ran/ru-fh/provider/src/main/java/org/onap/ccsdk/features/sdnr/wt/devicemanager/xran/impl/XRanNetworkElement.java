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
package org.onap.ccsdk.features.sdnr.wt.devicemanager.xran.impl;

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
public class XRanNetworkElement implements NetworkElement {

    private static final Logger log = LoggerFactory.getLogger(XRanNetworkElement.class);

    private final NetconfAccessor netconfAccessor;

    private final DataProvider databaseService;

    private final XRanToInternalDataModel xRanMapper;

    private ListenerRegistration<NotificationListener> xRanListenerRegistrationResult;
    private @NonNull final XRanChangeNotificationListener xRanListener;
    private ListenerRegistration<NotificationListener> xRanFaultListenerRegistrationResult;
    private @NonNull final XRanFaultNotificationListener xRanFaultListener;

    XRanNetworkElement(NetconfAccessor netconfAccess, DataProvider databaseService) {
        log.info("Create {}",XRanNetworkElement.class.getSimpleName());
        this.netconfAccessor = netconfAccess;
        this.databaseService = databaseService;

        this.xRanListenerRegistrationResult = null;
        this.xRanListener = new XRanChangeNotificationListener(netconfAccessor, databaseService);

        this.xRanFaultListenerRegistrationResult = null;
        this.xRanFaultListener = new XRanFaultNotificationListener();

        this.xRanMapper = new XRanToInternalDataModel();

    }

    public void initialReadFromNetworkElement() {
        Hardware hardware = readHardware(netconfAccessor);
        if (hardware != null) {
            List<Component> componentList = hardware.getComponent();
            if (componentList != null) {
                for (Component component : componentList) {
                    databaseService.writeInventory( xRanMapper.getInternalEquipment(netconfAccessor.getNodeId(), component));
                }
            }
        }
    }

    @Override
    public NetworkElementDeviceType getDeviceType() {
        return NetworkElementDeviceType.RAN;
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
        this.xRanListenerRegistrationResult = netconfAccessor.doRegisterNotificationListener(xRanListener);
        this.xRanFaultListenerRegistrationResult = netconfAccessor.doRegisterNotificationListener(xRanFaultListener);
        // Register netconf stream
        netconfAccessor.registerNotificationsStream(NetconfAccessor.DefaultNotificationsStream);


    }

    @Override
    public void deregister() {
        if (xRanListenerRegistrationResult != null) {
            this.xRanListenerRegistrationResult.close();
        }
        if (xRanFaultListenerRegistrationResult != null) {
            this.xRanFaultListenerRegistrationResult.close();
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
