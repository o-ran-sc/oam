package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.interfaceupfinfoitem.address;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.$YangModuleInfoImpl;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.interfaceupfinfoitem.Address;
import org.opendaylight.yangtools.yang.binding.Augmentable;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * case ipv4Address {
 *   leaf ipv4Address {
 *     type inet:ipv4-address;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/InterfaceUpfInfoItem/address/ipv4Address</i>
 *
 */
public interface Ipv4Address
    extends
    DataObject,
    Augmentable<Ipv4Address>,
    Address
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("ipv4Address");

    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.Ipv4Address</code> <code>ipv4Address</code>, or <code>null</code> if not present
     */
    org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.@Nullable Ipv4Address getIpv4Address();

}

