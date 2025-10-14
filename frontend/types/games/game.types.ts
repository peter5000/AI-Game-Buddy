export interface Action<T = { [k: string]: unknown }> {
    type: string;
    payload: T | null;
}

export interface GameState<
    MetaType = { [k: string]: unknown },
    PhaseType = Phase,
    PrivateStateType = PrivateStates,
> {
    game_id?: string;
    player_ids: string[];
    finished?: boolean;
    meta: MetaType;
    turn?: number | null;
    phase?: PhaseType | null;
    private_state?: PrivateStateType | null;
}

export interface Phase {
    current: string;
    /**
     * @minItems 1
     */
    available_phases: [string, ...string[]];
    _current_index: number;
}

export interface PrivateStates {
    states: {
        [k: string]: unknown;
    };
    [k: string]: unknown;
}
