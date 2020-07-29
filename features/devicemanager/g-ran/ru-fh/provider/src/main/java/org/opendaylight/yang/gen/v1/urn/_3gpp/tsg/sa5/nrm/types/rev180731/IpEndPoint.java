package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import java.lang.Integer;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.ipendpoint.Address;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * grouping ipEndPoint {
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
 *   }
 *   leaf transport {
 *     type t_TransportProtocol;
 *   }
 *   leaf port {
 *     type uint16;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/ipEndPoint</i>
 *
 */
public interface IpEndPoint
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("ipEndPoint");

    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.ipendpoint.Address</code> <code>address</code>, or <code>null</code> if not present
     */
    @Nullable Address getAddress();
    
    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.TTransportProtocol</code> <code>transport</code>, or <code>null</code> if not present
     */
    @Nullable TTransportProtocol getTransport();
    
    /**
     * @return <code>java.lang.Integer</code> <code>port</code>, or <code>null</code> if not present
     */
    @Nullable Integer getPort();

}

