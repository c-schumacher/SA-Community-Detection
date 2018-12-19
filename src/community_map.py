def community_map(comms, constrained_cols, full_cols):
    c_mapper = {}
    for i in constrained_cols:
        tmp = i.split(', ')
        tmp_idx = constrained_cols.index(i)
        if len(tmp) == 2:
            c_mapper[tmp[0]] = comms[tmp_idx]
            c_mapper[tmp[1]] = comms[tmp_idx]
        else:
            c_mapper[tmp[0]] = comms[tmp_idx]            
    new_comms = []
    for i in full_cols:
        new_comms.append(c_mapper[i])
    return np.array(new_comms)
