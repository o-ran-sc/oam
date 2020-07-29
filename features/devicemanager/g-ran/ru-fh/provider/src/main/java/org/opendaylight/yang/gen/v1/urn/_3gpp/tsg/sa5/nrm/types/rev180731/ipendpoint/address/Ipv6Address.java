package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.ipendpoint.address;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.$YangModuleInfoImpl;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.ipendpoint.Address;
import org.opendaylight.yangtools.yang.binding.Augmentable;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * case ipv6Address {
 *   leaf ipv6Address {
 *     type inet:ipv6-address;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/ipEndPoint/address/ipv6Address</i>
 *
 */
public interface Ipv6Address
    extends
    DataObject,
    Augmentable<Ipv6Address>,
    Address
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("ipv6Address");

    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.Ipv6Address</code> <code>ipv6Address</code>, or <code>null</code> if not present
     */
    org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.@Nullable Ipv6Address getIpv6Address();

}

