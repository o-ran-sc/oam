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
package org.onap.ccsdk.features.sdnr.wt.devicemanager.oran.test.mock;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.netconf.notifications.rev120206.NetconfConfigChange;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.netconf.notifications.rev120206.changed.by.parms.ChangedBy;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.netconf.notifications.rev120206.netconf.config.change.Edit;
import org.opendaylight.yangtools.yang.binding.Augmentation;
import org.opendaylight.yangtools.yang.binding.DataContainer;

public class NetconfConfigChangeMock implements NetconfConfigChange {

	@Override
	public Class<? extends DataContainer> getImplementedInterface() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public <E$$ extends Augmentation<NetconfConfigChange>> @Nullable E$$ augmentation(Class<E$$> augmentationType) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public @Nullable ChangedBy getChangedBy() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public @Nullable Datastore getDatastore() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public @Nullable List<Edit> getEdit() {
		List<Edit> list = new ArrayList<Edit>();
		return list;
	}

}
