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
    attributes = []
    if strength and strength > OutputThresholds.ATTRIBUTES.value:
        attributes.append(f"Str: {format_attribute(strength)}")
    if intelligence and intelligence > OutputThresholds.ATTRIBUTES.value:
        attributes.append(f"Int: {format_attribute(intelligence)}")
    if dexterity and dexterity > OutputThresholds.ATTRIBUTES.value:
        attributes.append(f"Dex: {format_attribute(dexterity)}")

    return output+", ".join(attributes)


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
