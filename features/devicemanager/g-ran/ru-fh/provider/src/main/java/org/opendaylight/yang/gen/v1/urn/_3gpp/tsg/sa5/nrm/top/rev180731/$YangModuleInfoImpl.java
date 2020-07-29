package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.top.rev180731;

import org.opendaylight.yangtools.yang.binding.ResourceYangModuleInfo;
import org.opendaylight.yangtools.yang.common.QName;
import org.opendaylight.yangtools.yang.binding.YangModuleInfo;
import java.util.Set;
import java.util.HashSet;
import com.google.common.collect.ImmutableSet;

public final class $YangModuleInfoImpl extends ResourceYangModuleInfo {
    private static final QName NAME = QName.create("urn:3gpp:tsg:sa5:nrm:Top", "2018-07-31", "_3gpp-common-top").intern();
    private static final YangModuleInfo INSTANCE = new $YangModuleInfoImpl();

    private final Set<YangModuleInfo> importedModules;

    public static YangModuleInfo getInstance() {
        return INSTANCE;
    }

    public static QName qnameOf(final java.lang.String localName) {
        return QName.create(NAME, localName).intern();
    }

    private $YangModuleInfoImpl() {
        Set<YangModuleInfo> set = new HashSet<>();
        set.add(org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.$YangModuleInfoImpl.getInstance());
        importedModules = ImmutableSet.copyOf(set);
    }

    @java.lang.Override
    public QName getName() {
        return NAME;
    }

    @java.lang.Override
    protected java.lang.String resourceName() {
        return "/META-INF/yang/_3gpp-common-top@2018-07-31.yang";
    }

    @java.lang.Override
    public Set<YangModuleInfo> getImportedModules() {
        return importedModules;
    }


}
