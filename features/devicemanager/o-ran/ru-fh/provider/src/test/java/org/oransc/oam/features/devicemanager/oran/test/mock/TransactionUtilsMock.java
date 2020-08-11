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

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;

import org.eclipse.jdt.annotation.Nullable;
import org.onap.ccsdk.features.sdnr.wt.netconfnodestateservice.TransactionUtils;
import org.opendaylight.mdsal.binding.api.DataBroker;
import org.opendaylight.mdsal.common.api.LogicalDatastoreType;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;

public class TransactionUtilsMock implements TransactionUtils {

	@Override
	public <T extends DataObject> @Nullable T readData(DataBroker dataBroker, LogicalDatastoreType dataStoreType,
			InstanceIdentifier<T> iid) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public <T extends DataObject> @Nullable T readDataOptionalWithStatus(DataBroker dataBroker,
			LogicalDatastoreType dataStoreType, InstanceIdentifier<T> iid, AtomicBoolean noErrorIndication,
			AtomicReference<String> statusIndicator) {
		// TODO Auto-generated method stub
		return null;
	}

}
