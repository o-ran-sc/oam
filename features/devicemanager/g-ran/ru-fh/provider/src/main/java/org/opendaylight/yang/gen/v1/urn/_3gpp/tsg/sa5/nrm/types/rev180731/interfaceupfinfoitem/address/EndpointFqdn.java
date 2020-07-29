package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.interfaceupfinfoitem.address;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.$YangModuleInfoImpl;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.interfaceupfinfoitem.Address;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.DomainName;
import org.opendaylight.yangtools.yang.binding.Augmentable;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * case endpointFqdn {
 *   leaf endpointFqdn {
 *     type inet:domain-name;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/InterfaceUpfInfoItem/address/endpointFqdn</i>
 *
 */
public interface EndpointFqdn
    extends
    DataObject,
    Augmentable<EndpointFqdn>,
    Address
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("endpointFqdn");

    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.DomainName</code> <code>endpointFqdn</code>, or <code>null</code> if not present
     */
    @Nullable DomainName getEndpointFqdn();

}

