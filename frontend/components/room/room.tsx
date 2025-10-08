// import { Chat } from "./chat";
import { GameContainer } from "../game-container";
import { Invite } from "./invite";
import { Players } from "./players";
import { Room as RoomType } from "@/types/room.types";

type RoomProps = {
    room_state: RoomType;
};

export function Room({ room_state }: RoomProps) {
    // Need to initialize chat and pass the state into components. Also need to pass in some callback after defining one

    // Need to pass in actual game component to game container, alternatively, game container could initialize the game component and description based on the title.

    // Need to pass in some callbacks to game container or game container could handle them.

    // In future, we might want to add functionality to kick players, mute players, etc.

    // Invite is unnecessary rn

    // Chat needs to get messages from some chat state

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-7xl mx-auto px-4 py-8">
            <GameContainer title={room_state.gameType} description={room_state.gameType} children="actual_game_placeholder"/>
            <div>
                <Players users={[...room_state.users]} creatorId={room_state.creatorId} />
                <Invite roomId={room_state.roomId} />
                {/* <Chat /> */}
            </div>
        </div>
    );
}