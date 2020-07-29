package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import com.google.common.base.MoreObjects;
import com.google.common.collect.ImmutableList;
import java.io.Serializable;
import java.lang.Override;
import java.lang.String;
import java.util.List;
import java.util.Objects;
import java.util.regex.Pattern;
import org.opendaylight.yangtools.yang.binding.CodeHelpers;
import org.opendaylight.yangtools.yang.binding.TypeObject;

public class TNCI
 implements TypeObject, Serializable {
    private static final long serialVersionUID = 6536694555014033331L;
    public static final List<String> PATTERN_CONSTANTS = ImmutableList.of("^(?:[01]*)$", "^(?:[a-fA-F0-9]*)$");
    private static final Pattern[] patterns = CodeHelpers.compilePatterns(PATTERN_CONSTANTS);
    private static final String[] regexes = { "[01]*", "[a-fA-F0-9]*" };
    private final String _string;


    private static void check_stringLength(final String value) {
        final int length = value.length();
        if (length == 36) {
            return;
        }
        CodeHelpers.throwInvalidLength("[[36..36]]", value);
    }
    public TNCI(String _string) {
        super();
        check_stringLength(_string);
        
        this._string = _string;
    }
    /**
     * Creates a copy from Source Object.
     *
     * @param source Source object
     */
    public TNCI(TNCI source) {
        this._string = source._string;
    }
    
    /**
     * Return a String representing the value of this union.
     *
     * @return String representation of this union's value.
     */
    public String stringValue() {
        if (_string != null) {
            return _string;
        }
    
        throw new IllegalStateException("No value assinged");
    }


    public String getString() {
        return _string;
    }


    @Override
    public int hashCode() {
        return CodeHelpers.wrapperHashCode(_string);
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
        TNCI other = (TNCI) obj;
        if (!Objects.equals(_string, other._string)) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        final MoreObjects.ToStringHelper helper = MoreObjects.toStringHelper(TNCI.class);
        CodeHelpers.appendValue(helper, "_string", _string);
        return helper.toString();
    }
}

