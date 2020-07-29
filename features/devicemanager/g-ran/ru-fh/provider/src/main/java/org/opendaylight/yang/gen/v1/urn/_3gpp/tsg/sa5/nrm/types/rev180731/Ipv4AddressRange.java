package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.Ipv4Address;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * grouping Ipv4AddressRange {
 *   leaf start {
 *     type inet:ipv4-address;
 *   }
 *   leaf end {
 *     type inet:ipv4-address;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/Ipv4AddressRange</i>
 *
 */
public interface Ipv4AddressRange
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("Ipv4AddressRange");

    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.Ipv4Address</code> <code>start</code>, or <code>null</code> if not present
     */
    @Nullable Ipv4Address getStart();
    
    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.Ipv4Address</code> <code>end</code>, or <code>null</code> if not present
     */
    @Nullable Ipv4Address getEnd();

}

