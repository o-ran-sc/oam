package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import com.google.common.collect.ImmutableMap;
import com.google.common.collect.ImmutableMap.Builder;
import java.lang.Integer;
import java.lang.Override;
import java.lang.String;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import org.opendaylight.yangtools.yang.binding.Enumeration;

public enum IsInitialBwp implements Enumeration {
    INITIAL(0, "INITIAL"),
    
    OTHER(1, "OTHER")
    ;

    private static final Map<String, IsInitialBwp> NAME_MAP;
    private static final Map<Integer, IsInitialBwp> VALUE_MAP;

    static {
        final Builder<String, IsInitialBwp> nb = ImmutableMap.builder();
        final Builder<Integer, IsInitialBwp> vb = ImmutableMap.builder();
        for (IsInitialBwp enumItem : IsInitialBwp.values()) {
            vb.put(enumItem.value, enumItem);
            nb.put(enumItem.name, enumItem);
        }

        NAME_MAP = nb.build();
        VALUE_MAP = vb.build();
    }

    private final String name;
    private final int value;

    private IsInitialBwp(int value, String name) {
        this.value = value;
        this.name = name;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public int getIntValue() {
        return value;
    }

    /**
     * Return the enumeration member whose {@link #getName()} matches specified value.
     *
     * @param name YANG assigned name
     * @return corresponding IsInitialBwp item, if present
     * @throws NullPointerException if name is null
     */
    public static Optional<IsInitialBwp> forName(String name) {
        return Optional.ofNullable(NAME_MAP.get(Objects.requireNonNull(name)));
    }

    /**
     * Return the enumeration member whose {@link #getIntValue()} matches specified value.
     *
     * @param intValue integer value
     * @return corresponding IsInitialBwp item, or null if no such item exists
     */
    public static IsInitialBwp forValue(int intValue) {
        return VALUE_MAP.get(intValue);
    }
}
