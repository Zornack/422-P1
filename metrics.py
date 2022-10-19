def compute_error_metrics(benchmark_ts, forecasted_ts):
    returnValue = None
    if (len(benchmark_ts) != len(forecasted_ts)):
        return_value = (-1, -1, -1, -1, -1)
        return return_value

    n = len(benchmark_ts)
    mean_abs_err = -1
    mean_ave_perc_err = -1
    symm_mean_ave_perc_err = -1
    mean_square_err = -1
    root_mean_square_err = -1

    # Check to see if timeseries contains vectors
    all_elems_vectors = timeseries_contains_vector(benchmark_ts, forecasted_ts)
    # Check to see if timeseries are comparable
    can_compare = can_compare_ts(benchmark_ts, forecasted_ts, all_elems_vectors)
    # timeseries contains vectors
    if (all_elems_vectors and can_compare):
        m = len(benchmark_ts[0])
        mean_abs_err = [0 for _ in range(m)]
        mean_ave_perc_err = [0 for _ in range(m)]
        symm_mean_ave_perc_err = [0 for _ in range(m)]
        mean_square_err = [0 for _ in range(m)]
        root_mean_square_err = [0 for _ in range(m)]
        num_zeros = 0
        for i in range(n):
            for j in range(m):
                mean_abs_err[j] += abs(benchmark_ts[i][j] - forecasted_ts[i][j])
                # Avoid division erron
                if (benchmark_ts[i][j] != 0):
                    mean_ave_perc_err[j] += 100 * abs(
                        (benchmark_ts[i][j] - forecasted_ts[i][j]) /
                        benchmark_ts[i][j])
                    symm_mean_ave_perc_err[j] += 100 * abs(
                        benchmark_ts[i][j] - forecasted_ts[i][j]) / ((abs(
                        benchmark_ts[i][j]) + abs(forecasted_ts[i][j])) / 2)
                else:
                    num_zeros += 1
                mean_square_err[j] += (benchmark_ts[i][j] - forecasted_ts[i][
                    j]) ** 2

        for k in range(m):
            mean_abs_err[k] = mean_abs_err[k] / n
            # avoid division error
            if (n - num_zeros != 0):
                mean_ave_perc_err[k] = mean_ave_perc_err[k] / (n - num_zeros)
                symm_mean_ave_perc_err[k] = symm_mean_ave_perc_err[k] / (
                            n - num_zeros)
            mean_square_err[k] = mean_square_err[k] / n
            root_mean_square_err[k] = (mean_square_err[k]) ** 0.5

    # timeseries contains scalars
    elif (can_compare):
        mean_abs_err = 0
        mean_ave_perc_err = 0
        symm_mean_ave_perc_err = 0
        mean_square_err = 0
        root_mean_square_err = 0
        num_zeros = 0
        for i in range(n):
            mean_abs_err += abs(benchmark_ts[i] - forecasted_ts[i])
            # avoid division error
            if (benchmark_ts[i] != 0):
                mean_ave_perc_err += 100 * abs(
                    (benchmark_ts[i] - forecasted_ts[i]) / benchmark_ts[i])
                symm_mean_ave_perc_err += 100 * abs(
                    benchmark_ts[i] - forecasted_ts[i]) / ((abs(
                    benchmark_ts[i]) + abs(forecasted_ts[i])) / 2)
            else:
                num_zeros += 1
            mean_square_err += (benchmark_ts[i] - forecasted_ts[i]) ** 2

        mean_abs_err = mean_abs_err / n
        # avoid division error
        if (n - num_zeros != 0):
            mean_ave_perc_err = mean_ave_perc_err / (n - num_zeros)
            symm_mean_ave_perc_err = symm_mean_ave_perc_err / (n - num_zeros)
        mean_square_err = mean_square_err / n
        root_mean_square_err = (mean_square_err) ** 0.5

    return_value = (
    mean_abs_err, mean_ave_perc_err, symm_mean_ave_perc_err, mean_square_err,
    root_mean_square_err)

    return return_value


def timeseries_contains_vector(benchmark_ts, forecasted_ts):
    return_value = True
    vec_len = -1
    n = len(benchmark_ts)
    # check to see if timeseries are composed of
    # vectors or scalars
    for i in range(n):
        b_ts_elem_type = type(benchmark_ts[i])
        f_ts_elem_type = type(forecasted_ts[i])
        if (b_ts_elem_type == int or b_ts_elem_type == float
                or f_ts_elem_type == int or f_ts_elem_type == float):
            return_value = False

        # Also check to see if ts vectors are same length
        if (return_value):
            if ((len(benchmark_ts[i]) != len(forecasted_ts[i])) or
                    (vec_len != -1 and len(forecasted_ts[i]) != vec_len)):
                return_value = False
                return return_value
            else:
                vec_len = len(benchmark_ts[i])
    return return_value


def can_compare_ts(benchmark_ts, forecasted_ts, all_elems_vectors):
    return_value = True
    n = len(benchmark_ts)

    if (all_elems_vectors):
        # make sure all vector elements are floats or ints
        m = len(benchmark_ts[0])
        for i in range(n):
            for j in range(m):
                types = (type(benchmark_ts[i][j]), type(forecasted_ts[i][j]))
                if ((types[0] != int and types[0] != float) or (
                (types[1] != int and types[1] != float))):
                    return_value = False
                    return return_value
    else:
        # make sure all elements are ints or floats
        for k in range(n):
            types = (type(benchmark_ts[k]), type(forecasted_ts[k]))
            if ((types[0] != int and types[0] != float) or (
            (types[1] != int and types[1] != float))):
                return_value = False
                return return_value
    return return_value