from poediscordbot.cogs.pob.poe_data.thresholds import OutputThresholds


def get_attributes(strength, intelligence, dexterity):
    """
    Display the attribute values if either of them meets the threshold defined in ~OutputThresholds.ATTRIBUTES
    :param strength: float value player strength
    :param intelligence: float value player intelligence
    :param dexterity: float value player dexterity
    :return: combined attributes string for embed usage
    """
    output = "**Attributes**: "
    if not strength:
        strength = 0
    if not intelligence:
        intelligence = 0
    if not dexterity:
        dexterity = 0

    if strength > OutputThresholds.ATTRIBUTES.value \
            or intelligence > OutputThresholds.ATTRIBUTES.value \
            or dexterity > OutputThresholds.ATTRIBUTES.value:
        return output + f"Str: {format_attribute(strength)}" \
               + f"Int: {format_attribute(intelligence)}" \
               + f"Dex: {format_attribute(dexterity)}"


def format_attribute(attribute):
    """
    If an attribute is above or equal to the threshold mark it in bold
    :param attribute: to mark up
    :return: bold or nonbold integer value of the attribute (rounded)
    """
    if attribute >= OutputThresholds.ATTRIBUTES.value:
        return f"**{attribute:.0f}**"
    else:
        return f"{attribute:.0f}"
