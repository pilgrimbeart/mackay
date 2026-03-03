function Div(el)
  if el.classes:includes("tribute") then
    local out = { pandoc.RawBlock("latex", "\\begin{tribute}") }
    for _, b in ipairs(el.content) do table.insert(out, b) end
    table.insert(out, pandoc.RawBlock("latex", "\\end{tribute}"))
    return out
  end

  if el.classes:includes("attrib") then
    local out = { pandoc.RawBlock("latex", "\\begin{flushright}\\itshape") }
    for _, b in ipairs(el.content) do table.insert(out, b) end
    table.insert(out, pandoc.RawBlock("latex", "\\end{flushright}"))
    return out
  end
end
