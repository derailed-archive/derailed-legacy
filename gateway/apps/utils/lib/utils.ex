defmodule Derailed.Utils do
  @spec struct_to_map(struct()) :: map()
  def struct_to_map(strct) do
    m = Map.from_struct(strct)
    Map.delete(m, :__meta__)
  end

  @spec map!(Postgrex.Result) :: list
  def map!(result) do
    case result do
      %{rows: []} ->
        []

      %{rows: [row], columns: columns} ->
        mapify(columns, row)

      _ ->
        raise "err"
    end
  end

  @spec maps!(Postgrex.Result) :: list
  def maps!(results) do
    case results do
      %{rows: []} ->
        []

      %{rows: rows, columns: columns} ->
        Enum.map(rows, fn row -> mapify(columns, row) end)

      _ ->
        raise "err"
    end
  end

  defp mapify(columns, row) do
    columns
    |> Enum.zip(row)
    |> Map.new()
  end
end
