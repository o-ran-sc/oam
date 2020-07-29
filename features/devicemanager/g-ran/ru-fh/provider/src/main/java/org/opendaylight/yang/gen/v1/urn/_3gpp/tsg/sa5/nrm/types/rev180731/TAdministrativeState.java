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

public enum TAdministrativeState implements Enumeration {
    /**
     * The resource is administratively prohibited from performingservices for its 
     * users.
     *
     */
    Locked(0, "Locked"),
    
    /**
     * Use of the resource is administratively permitted to existinginstances of use 
     * only. While the system remains in the shutting down statethe manager may at any 
     * time cause the managed object to revert to theunlocked state.
     *
     */
    Shutdown(1, "Shutdown"),
    
    /**
     * The resource is administratively permitted to perform services forits users. 
     * This is independent of its inherent operability.
     *
     */
    Unlocked(2, "Unlocked")
    ;

    private static final Map<String, TAdministrativeState> NAME_MAP;
    private static final Map<Integer, TAdministrativeState> VALUE_MAP;

    static {
        final Builder<String, TAdministrativeState> nb = ImmutableMap.builder();
        final Builder<Integer, TAdministrativeState> vb = ImmutableMap.builder();
        for (TAdministrativeState enumItem : TAdministrativeState.values()) {
            vb.put(enumItem.value, enumItem);
            nb.put(enumItem.name, enumItem);
        }

        NAME_MAP = nb.build();
        VALUE_MAP = vb.build();
    }

    private final String name;
    private final int value;

    private TAdministrativeState(int value, String name) {
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
     * @return corresponding TAdministrativeState item, if present
     * @throws NullPointerException if name is null
     */
    public static Optional<TAdministrativeState> forName(String name) {
        return Optional.ofNullable(NAME_MAP.get(Objects.requireNonNull(name)));
    }

    /**
     * Return the enumeration member whose {@link #getIntValue()} matches specified value.
     *
     * @param intValue integer value
     * @return corresponding TAdministrativeState item, or null if no such item exists
     */
    public static TAdministrativeState forValue(int intValue) {
        return VALUE_MAP.get(intValue);
    }
}
