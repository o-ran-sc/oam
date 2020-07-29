package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.Ipv6Prefix;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * grouping Ipv6PrefixRange {
 *   leaf start {
 *     type inet:ipv6-prefix;
 *   }
 *   leaf end {
 *     type inet:ipv6-prefix;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/Ipv6PrefixRange</i>
 *
 */
public interface Ipv6PrefixRange
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("Ipv6PrefixRange");

    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.Ipv6Prefix</code> <code>start</code>, or <code>null</code> if not present
     */
    @Nullable Ipv6Prefix getStart();
    
    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.Ipv6Prefix</code> <code>end</code>, or <code>null</code> if not present
     */
    @Nullable Ipv6Prefix getEnd();

}

