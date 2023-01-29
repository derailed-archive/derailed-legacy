defimpl Jsonrs.Encoder, for: [MapSet, Range, Stream] do
  def encode(struct), do: Enum.to_list(struct)
end
