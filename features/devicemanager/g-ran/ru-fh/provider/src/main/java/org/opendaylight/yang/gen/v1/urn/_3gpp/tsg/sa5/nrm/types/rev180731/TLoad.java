package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import com.google.common.base.MoreObjects;
import java.beans.ConstructorProperties;
import java.io.Serializable;
import java.lang.Override;
import java.lang.Short;
import java.lang.String;
import java.util.Objects;
import org.opendaylight.yangtools.yang.binding.CodeHelpers;
import org.opendaylight.yangtools.yang.binding.TypeObject;

public class TLoad
 implements TypeObject, Serializable {
    private static final long serialVersionUID = -1391841480548249841L;
    private final Short _value;

    private static void check_valueRange(final short value) {
        if (value >= (short)0 && value <= (short)100) {
            return;
        }
        CodeHelpers.throwInvalidRange("[[0..100]]", value);
    }

    @ConstructorProperties("value")
    public TLoad(Short _value) {
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
    public TLoad(TLoad source) {
        this._value = source._value;
    }

    public static TLoad getDefaultInstance(String defaultValue) {
        return new TLoad(Short.valueOf(defaultValue));
    }

    public Short getValue() {
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
        TLoad other = (TLoad) obj;
        if (!Objects.equals(_value, other._value)) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        final MoreObjects.ToStringHelper helper = MoreObjects.toStringHelper(TLoad.class);
        CodeHelpers.appendValue(helper, "_value", _value);
        return helper.toString();
    }
}

