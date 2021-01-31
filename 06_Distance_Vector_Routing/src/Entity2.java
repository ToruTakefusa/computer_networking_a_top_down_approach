public class Entity2 extends Entity {
    // Perform any necessary initialization in the constructor
    public Entity2() {
        initializeDistanceTable(999);
        this.distanceTable[2][0] = 3;
        this.distanceTable[2][1] = 1;
        this.distanceTable[2][2] = 0;
        this.distanceTable[2][3] = 2;

        int[] minCost = {this.distanceTable[2][0], this.distanceTable[2][1],
                this.distanceTable[2][2], this.distanceTable[2][3]};
        inform(minCost);
    }

    private void initializeDistanceTable(int value) {
        for (int i = 0; i < NetworkSimulator.NUM_ENTITIES; i++) {
            for (int j = 0; j < NetworkSimulator.NUM_ENTITIES; j++) {
                this.distanceTable[i][j] = 999;
            }
        }
    }

    // Handle updates when a packet is received.  Students will need to call
    // NetworkSimulator.toLayer2() with new packets based upon what they
    // send to update.  Be careful to construct the source and destination of
    // the packet correctly.  Read the warning in NetworkSimulator.java for more
    // details.
    public void update(Packet p) {
        if (p.getDest() != 2) return;

        setDistanceTable(p);

        var hasChanged = false;
        var oldCost = this.distanceTable[2][0];
        var newCost = Math.min(this.distanceTable[2][3] + this.distanceTable[3][0],
                this.distanceTable[2][1] + this.distanceTable[1][0]);
        if (oldCost > newCost) {
            hasChanged = true;
            this.distanceTable[2][0] = newCost;
        }

        oldCost = this.distanceTable[2][1];
        newCost = this.distanceTable[2][0] + this.distanceTable[0][1];
        if (oldCost > newCost) {
            hasChanged = true;
            this.distanceTable[2][1] = newCost;
        }

        oldCost = this.distanceTable[2][3];
        newCost = this.distanceTable[2][0] + this.distanceTable[0][3];
        if (oldCost > newCost) {
            hasChanged = true;
            this.distanceTable[2][3] = newCost;
        }

        printDT();
        if (!hasChanged) return;

        int[] cost = {this.distanceTable[2][0], this.distanceTable[2][1],
                this.distanceTable[2][2], this.distanceTable[2][3]};
        inform(cost);
    }

    private void inform(int[] cost) {
        NetworkSimulator.toLayer2(new Packet(2, 0, cost));
        NetworkSimulator.toLayer2(new Packet(2, 1, cost));
        NetworkSimulator.toLayer2(new Packet(2, 3, cost));
    }

    private void setDistanceTable(Packet p) {
        var source = p.getSource();
        this.distanceTable[source][0] = p.getMinCost(0);
        this.distanceTable[source][1] = p.getMinCost(1);
        this.distanceTable[source][2] = p.getMinCost(2);
        this.distanceTable[source][3] = p.getMinCost(3);
    }

    public void linkCostChangeHandler(int whichLink, int newCost) {
    }

    public void printDT() {
        System.out.println();
        System.out.println("           via");
        System.out.println(" D2 |   0   1   2   3");
        System.out.println("----+------------");
        for (int i = 0; i < NetworkSimulator.NUM_ENTITIES; i++) {
            System.out.print("   " + i + "|");
            for (int j = 0; j < NetworkSimulator.NUM_ENTITIES; j++) {
                if (distanceTable[i][j] < 10) {
                    System.out.print("   ");
                } else if (distanceTable[i][j] < 100) {
                    System.out.print("  ");
                } else {
                    System.out.print(" ");
                }
                System.out.print(distanceTable[i][j]);
            }
            System.out.println();
        }
    }
}