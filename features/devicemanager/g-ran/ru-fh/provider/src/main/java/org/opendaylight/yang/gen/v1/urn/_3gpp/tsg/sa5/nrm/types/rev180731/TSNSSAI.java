package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import com.google.common.base.MoreObjects;
import java.io.Serializable;
import java.lang.Long;
import java.lang.Override;
import java.lang.Short;
import java.lang.String;
import java.util.Objects;
import org.opendaylight.yangtools.yang.binding.CodeHelpers;
import org.opendaylight.yangtools.yang.binding.TypeObject;

public class TSNSSAI
 implements TypeObject, Serializable {
    private static final long serialVersionUID = -2943261658086489871L;
    private final Short _uint8;
    private final Long _uint32;


    private static void checkUint8Range(final short value) {
        if (value >= (short)0 && value <= (short)255) {
            return;
        }
        CodeHelpers.throwInvalidRange("[[0..255]]", value);
    }
    public TSNSSAI(Short _uint8) {
        super();
        checkUint8Range(_uint8);
        
        this._uint8 = _uint8;
        this._uint32 = null;
    }
    
    private static void checkUint32Range(final long value) {
        if (value >= 0L && value <= 4294967295L) {
            return;
        }
        CodeHelpers.throwInvalidRange("[[0..4294967295]]", value);
    }
    public TSNSSAI(Long _uint32) {
        super();
        checkUint32Range(_uint32);
        
        this._uint32 = _uint32;
        this._uint8 = null;
    }
    /**
     * Creates a copy from Source Object.
     *
     * @param source Source object
     */
    public TSNSSAI(TSNSSAI source) {
        this._uint8 = source._uint8;
        this._uint32 = source._uint32;
    }
    
    /**
     * Return a String representing the value of this union.
     *
     * @return String representation of this union's value.
     */
    public String stringValue() {
        if (_uint8 != null) {
            return _uint8.toString();
        }
        if (_uint32 != null) {
            return _uint32.toString();
        }
    
        throw new IllegalStateException("No value assinged");
    }


    public Short getUint8() {
        return _uint8;
    }
    
    public Long getUint32() {
        return _uint32;
    }


    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + Objects.hashCode(_uint8);
        result = prime * result + Objects.hashCode(_uint32);
        return result;
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
        TSNSSAI other = (TSNSSAI) obj;
        if (!Objects.equals(_uint8, other._uint8)) {
            return false;
        }
        if (!Objects.equals(_uint32, other._uint32)) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        final MoreObjects.ToStringHelper helper = MoreObjects.toStringHelper(TSNSSAI.class);
        CodeHelpers.appendValue(helper, "_uint8", _uint8);
        CodeHelpers.appendValue(helper, "_uint32", _uint32);
        return helper.toString();
    }
}

