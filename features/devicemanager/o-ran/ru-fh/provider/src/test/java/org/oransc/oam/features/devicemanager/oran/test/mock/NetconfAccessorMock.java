/*
 * ============LICENSE_START========================================================================
 * ONAP : ccsdk feature sdnr wt
 * =================================================================================================
 * Copyright (C) 2020 highstreet technologies GmbH Intellectual Property. All rights reserved.
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
package org.oransc.oam.features.devicemanager.oran.test.mock;

import com.google.common.util.concurrent.ListenableFuture;
import org.eclipse.jdt.annotation.NonNull;
import org.onap.ccsdk.features.sdnr.wt.netconfnodestateservice.Capabilities;
import org.onap.ccsdk.features.sdnr.wt.netconfnodestateservice.NetconfAccessor;
import org.onap.ccsdk.features.sdnr.wt.netconfnodestateservice.TransactionUtils;
import org.opendaylight.mdsal.binding.api.DataBroker;
import org.opendaylight.mdsal.binding.api.MountPoint;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.netconf.notification._1._0.rev080714.CreateSubscriptionOutput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNode;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.NodeId;
import org.opendaylight.yangtools.concepts.ListenerRegistration;
import org.opendaylight.yangtools.yang.binding.NotificationListener;
import org.opendaylight.yangtools.yang.common.RpcResult;

/**
 */
public class NetconfAccessorMock implements NetconfAccessor {

    private final NodeId nNodeId;
    private final NetconfNode netconfNode;
    private final MountPoint mountpoint;
    private final DataBroker netconfNodeDataBroker;

    public NetconfAccessorMock(NodeId nNodeId, NetconfNode netconfNode, MountPoint mountpoint,
            DataBroker netconfNodeDataBroker) {
        this.nNodeId = nNodeId;
        this.netconfNode = netconfNode;
        this.mountpoint = mountpoint;
        this.netconfNodeDataBroker = netconfNodeDataBroker;
    }

    @Override
    public NodeId getNodeId() {
        return nNodeId;
    }

    @Override
    public NetconfNode getNetconfNode() {
        return netconfNode;
    }

    @Override
    public Capabilities getCapabilites() {
        return null;
    }

    @Override
    public DataBroker getDataBroker() {
        return netconfNodeDataBroker;
    }

    @Override
    public MountPoint getMountpoint() {
        return mountpoint;
    }

    @Override
    public TransactionUtils getTransactionUtils() {
        return null;
    }

    @Override
    public <T extends NotificationListener> ListenerRegistration<NotificationListener> doRegisterNotificationListener(
            @NonNull T listener) {
        return null;
    }

    @Override
    public ListenableFuture<RpcResult<CreateSubscriptionOutput>> registerNotificationsStream(String streamName) {
        return null;
    }

}
