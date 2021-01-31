public class Packet {
    private int source;
    private int dest;
    private int[] mincost;

    public Packet(Packet p) {
        source = p.getSource();
        dest = p.getDest();
        mincost = new int[NetworkSimulator.NUM_ENTITIES];
        for (int i = 0; i < NetworkSimulator.NUM_ENTITIES; i++) {
            mincost[i] = p.getMinCost(i);
        }
    }

    public Packet(int s, int d, int[] mc) {
        source = s;
        dest = d;

        mincost = new int[NetworkSimulator.NUM_ENTITIES];
        if (mc.length != NetworkSimulator.NUM_ENTITIES) {
            System.out.println("Packet(): Invalid data format.");
            System.exit(1);
        }

        for (int i = 0; i < NetworkSimulator.NUM_ENTITIES; i++) {
            mincost[i] = mc[i];
        }
    }

    public int getSource() {
        return source;
    }

    public int getDest() {
        return dest;
    }

    public int getMinCost(int ent) {
        return mincost[ent];
    }

    public String toString() {
        String str;
        str = "source: " + source + "  dest: " + dest + "  mincosts: ";

        for (int i = 0; i < NetworkSimulator.NUM_ENTITIES; i++) {
            str = str + i + "=" + getMinCost(i) + " ";
        }

        return str;

    }

}