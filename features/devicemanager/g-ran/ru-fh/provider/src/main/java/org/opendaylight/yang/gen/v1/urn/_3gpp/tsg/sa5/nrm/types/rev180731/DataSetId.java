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

public enum DataSetId implements Enumeration {
    SUBSCRIPTION(0, "SUBSCRIPTION"),
    
    POLICY(1, "POLICY"),
    
    EXPOSURE(2, "EXPOSURE"),
    
    APPLICATION(3, "APPLICATION")
    ;

    private static final Map<String, DataSetId> NAME_MAP;
    private static final Map<Integer, DataSetId> VALUE_MAP;

    static {
        final Builder<String, DataSetId> nb = ImmutableMap.builder();
        final Builder<Integer, DataSetId> vb = ImmutableMap.builder();
        for (DataSetId enumItem : DataSetId.values()) {
            vb.put(enumItem.value, enumItem);
            nb.put(enumItem.name, enumItem);
        }

        NAME_MAP = nb.build();
        VALUE_MAP = vb.build();
    }

    private final String name;
    private final int value;

    private DataSetId(int value, String name) {
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
     * @return corresponding DataSetId item, if present
     * @throws NullPointerException if name is null
     */
    public static Optional<DataSetId> forName(String name) {
        return Optional.ofNullable(NAME_MAP.get(Objects.requireNonNull(name)));
    }

    /**
     * Return the enumeration member whose {@link #getIntValue()} matches specified value.
     *
     * @param intValue integer value
     * @return corresponding DataSetId item, or null if no such item exists
     */
    public static DataSetId forValue(int intValue) {
        return VALUE_MAP.get(intValue);
    }
}
