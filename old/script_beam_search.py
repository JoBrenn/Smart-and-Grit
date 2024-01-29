def beamsearch_tuning(district_number: int, runs: int, max_beam: int):
    print("Start Beam Search tuning")
    district = District(district_number, "costs-own")
    if os.path.isfile(f'output/pickle/District{district_number}-Runs{runs}-MaxBeam{max_beam}-outcomes.pkl'):
        with open(f'output/pickle/District{district_number}-Runs{runs}-MaxBeam{max_beam}-outcomes.pkl', "rb") as infile:
            outcomes = pickle.load(infile)
        with open(f'output/pickle/District{district_number}-Runs{runs}-MaxBeam{max_beam}-best_states.pkl', "rb") as infile:
            best_states = pickle.load(infile)
        print("Loaded pickled files")
        if outcomes:
            start_beam = max(outcomes)
            start_runs_at = len(outcomes[start_beam])
        else:
            start_beam = 1
            start_runs_at = 0
    else:
        outcomes = {}
        best_states = {}
        start_beam = 1
        start_runs_at = 0

    with open(f"output/csv/District{district_number}-Runs{runs}-MaxBeam{max_beam}.csv", "w", newline="") as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(["beam","valid-runs","costs"])

    # try:
    for beam in range(start_beam, max_beam + 1):
        for i in range(start_runs_at, runs):
            seed(i)
            beamsearch = BeamSearch(district, beam)
            output = beamsearch.run()
            if output:
                output_cost = output.return_cost()
            else:
                output_cost = 0

            if beam in outcomes:
                outcomes[beam].append(output_cost)
            else:
                outcomes[beam] = [output_cost]

            if output_cost == max(outcomes[beam]) and output:
                best_states[beam] = output.return_output()

            start_runs_at = 0

        if outcomes[beam]:
            valid_outcomes = len(outcomes[beam]) - outcomes[beam].count(0)
            print("Valid outcomes:", valid_outcomes)
        else:
            valid_outcomes = 0

        with open(f"output/csv/District{district_number}-Runs{runs}-MaxBeam{max_beam}.csv", "a", newline="") as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow([beam, valid_outcomes, outcomes[beam]])

    # except Exception as e:
    #     print("Hello")
    #     print(e, file=sys.stderr)
    #     with open(f'output/pickle/District{district_number}-Runs{runs}-MaxBeam{max_beam}-outcomes.pkl', 'wb') as outfile:
    #         pickle.dump(outcomes, outfile)
    #     with open(f'output/pickle/District{district_number}-Runs{runs}-MaxBeam{max_beam}-best_states.pkl', 'wb') as outfile:
    #         pickle.dump(best_states, outfile)


    with open(f"output/csv/District{district_number}-Runs{runs}-MaxBeam{max_beam}.csv", "w", newline="") as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(["beam","valid-runs","costs"])
        for beam in outcomes:
            valid_outcomes = 0
            for outcome in outcomes[beam]:
                if outcome:
                    valid_outcomes += 1
            writer.writerow([beam, valid_outcomes, outcomes[beam]])
    with open(f"output/JSON/District{district_number}-Runs{runs}-MaxBeam{max_beam}.json", "w") as outfile:
        dump(best_states, outfile, indent=6)

    print(outcomes)
    exit()

    return outcomes
