package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.guami;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.$YangModuleInfoImpl;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.AMFIdentifier;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.Guami;
import org.opendaylight.yangtools.yang.binding.Augmentable;
import org.opendaylight.yangtools.yang.binding.ChildOf;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * container amfId {
 *   uses aMFIdentifier;
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/Guami/amfId</i>
 *
 * <p>To create instances of this class use {@link AmfIdBuilder}.
 * @see AmfIdBuilder
 *
 */
public interface AmfId
    extends
    ChildOf<Guami>,
    Augmentable<AmfId>,
    AMFIdentifier
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("amfId");


}

