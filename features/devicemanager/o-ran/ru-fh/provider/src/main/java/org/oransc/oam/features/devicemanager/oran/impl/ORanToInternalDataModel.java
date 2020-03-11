/**
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

import java.util.ArrayList;
import java.util.List;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.hardware.rev180313.hardware.Component;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.data.provider.rev190801.Inventory;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.data.provider.rev190801.InventoryBuilder;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.NodeId;

/**
 * @author herbert
 *
 */
public class ORanToInternalDataModel {


    public Inventory getInternalEquipment(NodeId nodeId, Component component) {

        InventoryBuilder inventoryBuilder = new InventoryBuilder();

        // General
        inventoryBuilder.setNodeId(nodeId.getValue());
        inventoryBuilder.setParentUuid(component.getParent());
        inventoryBuilder.setTreeLevel(new Long(component.getParentRelPos()));

        inventoryBuilder.setUuid(component.getUuid().getValue());
        // -- String list with ids of holders
        List<String> containerHolderKeyList = new ArrayList<>();
        List<String> containerHolderList = component.getContainsChild();
        if (containerHolderList != null) {
            for (String containerHolder : containerHolderList) {
                containerHolderKeyList.add(containerHolder);
            }
        }
        inventoryBuilder.setContainedHolder(containerHolderKeyList);
        // -- Manufacturer related things
        inventoryBuilder.setManufacturerName(component.getName());

        // Equipment type
        inventoryBuilder.setDescription(component.getDescription());
        inventoryBuilder.setModelIdentifier(component.getModelName());
        inventoryBuilder.setPartTypeId(component.getXmlClass().getName());
        inventoryBuilder.setTypeName(component.getName());
        inventoryBuilder.setVersion(component.getHardwareRev());

        // Equipment instance
        inventoryBuilder.setDate(component.getMfgDate().getValue());
        inventoryBuilder.setSerial(component.getSerialNum());

        return inventoryBuilder.build();
    }

}
