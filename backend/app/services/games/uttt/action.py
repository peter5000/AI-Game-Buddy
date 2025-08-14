from app.services.games.uttt.constants import X_STATE_VALUE, O_STATE_VALUE
from pydantic import BaseModel

class Action(BaseModel):
    symbol: int
    index: int
    def is_symbol_X(self) -> bool:
        return self.symbol == X_STATE_VALUE

    def is_symbol_O(self) -> bool:
        return self.symbol == O_STATE_VALUE

    def __str__(self):
        output = '{cls}(symbol={symbol}, index={index})'
        output = output.format(
            cls=self.__class__.__name__,
            symbol={X_STATE_VALUE: 'X', O_STATE_VALUE: 'O'}[self.symbol],
            index=self.index,
        )
        return output