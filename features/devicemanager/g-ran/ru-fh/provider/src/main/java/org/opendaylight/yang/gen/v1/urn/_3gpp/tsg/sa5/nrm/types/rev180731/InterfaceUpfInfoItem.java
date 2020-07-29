package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import java.lang.String;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.interfaceupfinfoitem.Address;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * grouping InterfaceUpfInfoItem {
 *   leaf interfaceType {
 *     type UPInterfaceType;
 *   }
 *   choice address {
 *     case ipv4Address {
 *       leaf ipv4Address {
 *         type inet:ipv4-address;
 *       }
 *     }
 *     case ipv6Address {
 *       leaf ipv6Address {
 *         type inet:ipv6-address;
 *       }
 *     }
 *     case ipv6Prefix {
 *       leaf ipv6Prefix {
 *         type inet:ipv6-prefix;
 *       }
 *     }
 *     case endpointFqdn {
 *       leaf endpointFqdn {
 *         type inet:domain-name;
 *       }
 *     }
 *   }
 *   leaf networkInstance {
 *     type string;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/InterfaceUpfInfoItem</i>
 *
 */
public interface InterfaceUpfInfoItem
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("InterfaceUpfInfoItem");

    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.UPInterfaceType</code> <code>interfaceType</code>, or <code>null</code> if not present
     */
    @Nullable UPInterfaceType getInterfaceType();
    
    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.interfaceupfinfoitem.Address</code> <code>address</code>, or <code>null</code> if not present
     */
    @Nullable Address getAddress();
    
    /**
     * @return <code>java.lang.String</code> <code>networkInstance</code>, or <code>null</code> if not present
     */
    @Nullable String getNetworkInstance();

}

