package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.Uri;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * grouping defaultNotificationSubscription {
 *   leaf notificationType {
 *     type NotificationType;
 *   }
 *   leaf callbackUri {
 *     type inet:uri;
 *   }
 *   leaf n1MessageClass {
 *     type N1MessageClass;
 *   }
 *   leaf n2InformationClass {
 *     type N2InformationClass;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/defaultNotificationSubscription</i>
 *
 */
public interface DefaultNotificationSubscription
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("defaultNotificationSubscription");

    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.NotificationType</code> <code>notificationType</code>, or <code>null</code> if not present
     */
    @Nullable NotificationType getNotificationType();
    
    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.Uri</code> <code>callbackUri</code>, or <code>null</code> if not present
     */
    @Nullable Uri getCallbackUri();
    
    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.N1MessageClass</code> <code>n1MessageClass</code>, or <code>null</code> if not present
     */
    @Nullable N1MessageClass getN1MessageClass();
    
    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.N2InformationClass</code> <code>n2InformationClass</code>, or <code>null</code> if not present
     */
    @Nullable N2InformationClass getN2InformationClass();

}

