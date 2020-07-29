package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import com.google.common.base.MoreObjects;
import java.beans.ConstructorProperties;
import java.io.Serializable;
import java.lang.Long;
import java.lang.Override;
import java.lang.String;
import java.util.Objects;
import org.opendaylight.yangtools.yang.binding.CodeHelpers;
import org.opendaylight.yangtools.yang.binding.TypeObject;

public class TNRPCI
 implements TypeObject, Serializable {
    private static final long serialVersionUID = -8223745380422869872L;
    private final Long _value;

    private static void check_valueRange(final long value) {
        if (value >= 0L && value <= 4294967295L) {
            return;
        }
        CodeHelpers.throwInvalidRange("[[0..4294967295]]", value);
    }

    @ConstructorProperties("value")
    public TNRPCI(Long _value) {
        if (_value != null) {
            check_valueRange(_value);
        }
    
        Objects.requireNonNull(_value, "Supplied value may not be null");
    
        this._value = _value;
    }
    
    /**
     * Creates a copy from Source Object.
     *
     * @param source Source object
     */
    public TNRPCI(TNRPCI source) {
        this._value = source._value;
    }

    public static TNRPCI getDefaultInstance(String defaultValue) {
        return new TNRPCI(Long.valueOf(defaultValue));
    }

    public Long getValue() {
        return _value;
    }


    @Override
    public int hashCode() {
        return CodeHelpers.wrapperHashCode(_value);
    }

    @Override
    public boolean equals(java.lang.Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        TNRPCI other = (TNRPCI) obj;
        if (!Objects.equals(_value, other._value)) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        final MoreObjects.ToStringHelper helper = MoreObjects.toStringHelper(TNRPCI.class);
        CodeHelpers.appendValue(helper, "_value", _value);
        return helper.toString();
    }
}

