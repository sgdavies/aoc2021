class Day06 {
    public static void main(String[] args) {
	final int end = Integer.parseInt(args[0]);
	String test = "3,4,3,1,2";
	String data = "1,1,1,1,1,1,1,4,1,2,1,1,4,1,1,1,5,1,1,1,1,1,1,1,1,1,1,1,1,5,1,1,1,1,3,1,1,2,1,2,1,3,3,4,1,4,1,1,3,1,1,5,1,1,1,1,4,1,1,5,1,1,1,4,1,5,1,1,1,3,1,1,5,3,1,1,1,1,1,4,1,1,1,1,1,2,4,1,1,1,1,4,1,2,2,1,1,1,3,1,2,5,1,4,1,1,1,3,1,1,4,1,1,1,1,1,1,1,4,1,1,4,1,1,1,1,1,1,1,2,1,1,5,1,1,1,4,1,1,5,1,1,5,3,3,5,3,1,1,1,4,1,1,1,1,1,1,5,3,1,2,1,1,1,4,1,3,1,5,1,1,2,1,1,1,1,1,5,1,1,1,1,1,2,1,1,1,1,4,3,2,1,2,4,1,3,1,5,1,2,1,4,1,1,1,1,1,3,1,4,1,1,1,1,3,1,3,3,1,4,3,4,1,1,1,1,5,1,3,3,2,5,3,1,1,3,1,3,1,1,1,1,4,1,1,1,1,3,1,5,1,1,1,4,4,1,1,5,5,2,4,5,1,1,1,1,5,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,5,1,1,1,1,1,1,3,1,1,2,1,1";

	System.out.println(simulate(test, end));
	System.out.println(simulate(data, end));
    }

    static long simulate(String input, int end) {
	long[] fish = new long[end + 1 + 8];
	for (String f : input.split(",")) {
		int d = Integer.parseInt(f);
		fish[d] += 1;
	}
	for (int day = 0; day < end; day++) {
		fish[day+7] += fish[day];
		fish[day+1+8] += fish[day];
	}
	long sum = 0;
	for (int i=0; i<9; i++) {
		sum += fish[end+i];
	}
	return sum;
    }
}
