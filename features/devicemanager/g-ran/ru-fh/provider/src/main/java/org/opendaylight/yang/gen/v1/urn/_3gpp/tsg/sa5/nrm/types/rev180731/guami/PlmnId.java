package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.guami;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.$YangModuleInfoImpl;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.Guami;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.PLMNId;
import org.opendaylight.yangtools.yang.binding.Augmentable;
import org.opendaylight.yangtools.yang.binding.ChildOf;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * container plmnId {
 *   uses pLMNId;
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/Guami/plmnId</i>
 *
 * <p>To create instances of this class use {@link PlmnIdBuilder}.
 * @see PlmnIdBuilder
 *
 */
public interface PlmnId
    extends
    ChildOf<Guami>,
    Augmentable<PlmnId>,
    PLMNId
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("plmnId");


}

