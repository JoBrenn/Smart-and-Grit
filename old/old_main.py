# At least 1 argument
if len(sys.argv) < 2 or len(sys.argv) > 5:
    print("Usage: python3 main.py <district> --<method> [options]")
elif sys.argv[1] == "--load":
    try:
        if sys.argv[2] == "--format":
            with open("output/output-format.json", "r") as f:
                content = f.read()
                data = json.loads(content)
        # elif sys.argv[2] == "--empty":
        #     with open(f"data/district_{sys.argv[3]}{sys.argv[2]}", "r") as f:
        #         content = f.read()
        #         data = json.loads(content)
        else:
            with open(f"output/JSON/{sys.argv[2]}", "r") as f:
                content = f.read()
                data = json.loads(content)
        plot_output(data)
    except:
        print("Usage: python3 --load <JSON_file>")

# Shows format output
elif sys.argv[1] == "--format":
    data = load_JSON_output("output/output-format.json")
    plot_output(data)
# Shows the user a manual
elif sys.argv[1] == "--help":
        print("Usage: python3 main.py <district> --[method]")
        print("Methods:")
        print("  --help:\t\t Display help manual")
        print("  --format:\t\t Display formatted output")
        print("  --h[isto[gram]]:\t Get histogram of N runs of random assignment Manhattan distance algorithm.")
        print("  --randrwalk:\t\t Randomly assigns houses to batteries. " + \
                            "Creates cable path through randomly taking random steps until destination is reached.")
        print("  --randmanh:\t\t Randomly assigns houses to batteries. \t\t\t\t(Manhattan Distance)")
        print("  --greedmanh:\t\t Uses greedy algorithm to assign houses to batteries. \t\t(Manhattan Distance)")
        print("  --greedmanhcap:\t Uses greedy algorithm to assign houses to capped batteries. \t(Manhattan Distance) ")
elif sys.argv[1] in ["--h", "--histo", "--histogram"]:
    if len(sys.argv) < 4 or sys.argv[2] == "--help" or \
     not sys.argv[3].isnumeric() or not 1 <= int(sys.argv[3]) <= 3:
        print("Usage: python3 main.py --histogram --<method> <district> [runs]")
    else:
        # Default value
        runs = 100

        if len(sys.argv) == 4:
            alg_method = sys.argv[2]
            district_number = int(sys.argv[3])
        elif len(sys.argv) == 5:
            alg_method = sys.argv[2]
            district_number = int(sys.argv[3])
            runs = int(sys.argv[4])

        outputs = runs_algorithms_to_costs(district_number, runs, alg_method)
        plot_output_histogram(outputs, alg_method, runs, district_number)

# Shows output of one district between 1 - 3
elif sys.argv[1] in ["--randmanh", "--randmanhcap", "--randrwalk", "--greedmanh", "--hillclimb"]:
    if len(sys.argv) < 3 or sys.argv[2] == "--help" or not sys.argv[2].isnumeric():
        print("Usage: python3 main.py --<method> <district>")
    else:
        alg_method = sys.argv[1]
        district_number = int(sys.argv[2])
        district = District(district_number, "costs-own")
        cost_type = "costs-own"

        # Run different methods based on user input
        if alg_method == "--randrwalk":
            """
                Here we apply a random assignment of houses to batteries,
                not taking the capacity into account. Furthermore is a
                random walk used for the connections between house and
                batttery.
                Takes quite some time and is really messy in visualisation,
                so we only take the first house into account.
            """

            output = run_random_assignment_random_walk(district)
            merge = False
            method = "Random + random walk"

        elif alg_method == "--randmanh":
            """
                Here we again apply a random assignment of houses to batteries,
                not taking the capacity into account. Instead of a random walk,
                we now implement the shortest Manhattan distance.
            """
            output = run_random_assignment_shortest_distance(district, cost_type)
            assignment = random_assignment
            method = "Random + Manhattan"
            # print(output)
            print(output[0]["costs-own"])

        elif alg_method == "--randmanhcap":
            """
                Here we again apply a random assignment of houses to batteries,
                not taking the capacity into account. Instead of a random walk,
                we now implement the shortest Manhattan distance.
            """

            assignment = random_assignment_capacity
            method = "Random + Manhattan + Capacity"
            merge = False
            print(district.is_valid())

        elif alg_method == "--greedmanh":
            """
                Here we apply a greedy algorithm. A house is assigned to the battery,
                starting at a random house, with the most capacity left.
                The path of the cable is created using the shortest Manhattan distance
                from the house towards the battery
            """

            #output = run_greedy_assignment_shortest_walk(district, method)
            assignment = greedy_assignment
            merge = True

            # print(f"The cost for greedy assignment and shortest Manhattan distance in district {district.district} is {district.return_cost()}.")
            method = "Greedy + Manhattan"

        elif alg_method == "--hillclimb":
            """
                Here we apply a Hillclimber algorithm. We start with a random configuration
                of house-battery connections by Manhattan distance. We change one house-battery
                connection and check whether this lowers the costs
                until we come across a valid solution to our problem. From there
                we randomly swap two house-battery connections and check whether the solution
                is still valid and the cost is lowered.
                Give integer of number of iterations in command line before indicating district number
            """

            n = int(sys.argv[3])
            print(n)
            hillclimb = HillClimber(district)
            output = hillclimb.run_hill_climber(district, n, 1000).return_output()

        if alg_method != "--randrwalk":
            output = run_alg_manh(district, assignment, merge, cost_type)

        # Write output to JSON file
        write_output_to_JSON(output, alg_method[2:], district_number)

        # Plot the output
        plot_output(output, alg_method, district_number, method)



else:
    print("Invalid input.")
