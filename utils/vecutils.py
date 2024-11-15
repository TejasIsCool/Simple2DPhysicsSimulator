from py5 import Py5Vector


class VecUtils:
    """
    Just a useful list of vector functions
    """

    @staticmethod
    def projection(a: Py5Vector, b: Py5Vector) -> Py5Vector:
        """
        Returns a projection vector of on b (A vector in direction of b, with the projected magnitude of a on b)
        :param a: Vector that get projected onto the other
        :param b: The vector along which the projected vector lies on
        :return: The resulting projected vector
        """
        # Formula is
        # ⎛ a • b̲ ⎞ b̲
        # ⎝    |b|⎠|b|
        # (Projection * normalised vector along b)
        # Which simplifies down to below
        return (a.dot(b)/b.mag_sq)*b